# This script can be execute by windows powershell.

<#
Define Comment-Based Help for Script, which can print out by using Get-Help(insensitive-case) cmdlet (that is
a special type of command provided in the Windows PowerShell command line environment), example:

PS> Get-Help .\docker-swarm.ps1 -Full

* if you faced an error that incorrect or not like what expect help text to be, this because you need to load the script
into system memory before using Get-Help tool:

PS> . .\deploy-swarm.ps1

* then run:

PS> Get-Help .\docker-swarm.ps1 -Full

#>

<#
.SYNOPSIS

Deploy stack of services to Docker swarm.

.DESCRIPTION

Deploy stack of services to Docker swarm.
Takes two optional arguments: -ComposeFile, -StackName.

.PARAMETER ComposeFile
Specifies the docker-compose file.

.PARAMETER StackName
Specifies the string as name that will represent the stack in docker swarm.

.INPUTS

None. You can't use .NET types of objects that can be piped to the function or script.

.OUTPUTS

None.

.EXAMPLE

To run the script file while it is found at same directory:
PS> .\deploy.swarm.ps1 [-ComposeFile "docker-compose.yml"] [-StackName "YourProjectName"]

.EXAMPLE

To run the script file while is found at another directory:
PS> path/to/deploy.swarm.ps1 [-ComposeFile "docker-compose.yml"] [-StackName "YourProjectName"]
#>

<#
To define parameters in a script, use a 'Param' statement. The Param statement must be the first statement
in a script, except for comments and any #Require statements.
Script parameters work like function parameters. The parameter values are available to all of the commands
in the script. All of the features of function parameters, including the Parameter attribute and its named
arguments, are also valid in scripts.
#>

<# Here we define two parameters as required (Mandatory) to execute the script and at same time each one has default value.

Note: if specify the parameter as specific data type like:

[string][Parameter(Mandatory)] $ComposeFile="docker-compose.yml"

you gonna face an issue when execute the command without specifying the arguments which the shell will ask you to set
a value for each required argument, if you specify an empty value this will count as value and no default value can
be use because and an that time an error will raise:

ParameterBindingValidationException

which means the shell can't bind an empty string with a required string value even if it has default value.

Info: the default value will be use when run the shell like below:

.\deploy.swarm.ps1 -ComposeFile -StackName

#>
param (
    [Parameter(Mandatory)] $ComposeFile="docker-compose.yml",
    [Parameter(Mandatory)] $StackName="ecommerce"
)

# Check whether the arguments that required are specified as empty string or not, if so, then specify a default value
# for parameter.
if($ComposeFile -eq ""){
    $ComposeFile = "docker-compose.yml"
    Write-Output "Set default value for -ComposeFile argument: $ComposeFile"
}

if($StackName -eq ""){
    $StackName = "ecommerce"
    Write-Output "Set default value for -StackName argument: $StackName"
}

<#
Define a variable that represent the content of env file by using the 'Get-Content' command tool which is similar to 'cat'
command tool in linux system.
#>
$envFileContent = Get-Content -Path .env

# Loop over each line of $envFileContent
# Note: each {} represent a block of statement.
ForEach ($line in $envFileContent){
     if($line){
          # split the line by assignment mark (=), and return a list.
          $varNameValSplit = $line.Split("=")
          # Check if list have two items which means there is a variable and value for it.
          if($varNameValSplit.Length -eq 2){
            $varName = $varNameValSplit[0]
            # Trim double quotes from both sides of the string in case it's exist.
            $varVal = $varNameValSplit[1].Trim('"')
            # Using $varName and $varValSet, set environment variable in system memory that
            # can be use later by 'docker stack deploy' command.
            [Environment]::SetEnvironmentVariable($varName, $varVal)
            # Print on the screen that a environment variable has been set.
            Write-Output "Set var $varName"
          }
     }
}

<#
Run the 'docker stack deploy' command with the provided arguments value and using the environment variables for
docker-compose file from the system.
#>
docker stack deploy --compose-file $ComposeFile --with-registry-auth $StackName