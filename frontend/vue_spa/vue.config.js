/*
The django-vue connection approach of which this configuration is part of was made
popular by Ejez and EugeneDae. You can find more information about them here:
https://github.com/django-webpack/django-webpack-loader/issues/209#issue-512863855
https://github.com/EugeneDae/django-vue-cli-webpack-demo
I however decided to simplify things a little by avoiding template inheritance
on Django's side, as this is not needed in our scenario and, I believe, in most
such cases.
Note: please remember you will also need to properly configure your Django
backend for this setup to work as expected both in development and production.
Settings Options:
https://cli.vuejs.org/config/
https://v4.webpack.js.org/configuration/dev-server/
https://github.com/webpack/webpack-dev-server/blob/master/migration-v4.md
*/

/*
Hot Reload is always enabled except following situations:
1- webpack target is node (SSR)
2- webpack minifies the code
3- process.env.NODE_ENV === 'production'
*/

const { defineConfig } = require('@vue/cli-service');
const path = require(`path`);

module.exports = defineConfig({
  /*
  By default, babel-loader ignores all files inside node_modules. You can
  enable this option to avoid unexpected untranspiled code from third-party
  dependencies.
  */
  transpileDependencies: true,

  // The base URL your application bundle will be deployed at.
  publicPath:
    // When run 'npm run build' command, will set 'NODE_ENV' variable to 'production' value.
    // Note: if you used "./" as public path means all created urls for static files (js, css and images) will
    //       start with no slash:
    //       <meta name="msapplication-TileImage" content="img/something.png">
    //
    //       if you used "/dist/" as public path:
    //       <meta name="msapplication-TileImage" content="/dist/img/something.png">
    //
    // Important: if you face the following error while trying to load the index.html file:
    //
    //            Uncaught SyntaxError: Unexpected token '<'
    //
    //            This is because the urls those generated in build process for production of static files
    //            is not the same path as stored in nginx server where can be served to client. in other words the
    //            root in nginx should have the url path of static file like:
    //            /img/something.png
    process.env.NODE_ENV === "production" ? "/" : "http://127.0.0.1:8080",

  // Specify pages of your project frontend.
  // Note: our project is Single Page App.
  pages: {
    index: {
      // entry of js file for the index page
      entry: 'src/main.js',
      // the source template
      template: 'public/index.html',
      // output as dist/index.html
      filename: 'index.html',
      /*
      The html template <title></title> tag needs to be:

      <title><%= htmlWebpackPlugin.options.title %></title>

      so the 'name' variable value in 'package.json' file that could be used as default value
      for title tag can be overwritten by this option value which we set here.
      */
      title: 'Jamie and Cassie',
      /*
      chunks to include on this page, by default includes extracted common
      chunks and vendor chunks.
      */
      chunks: ['chunk-vendors', 'chunk-common', 'index']
    },
  },

  // Configure aliases to use by Webpack server at build time.
  configureWebpack: {
    // resolve: {
    //   alias: {
    //     // '<symbol_or_dependency_name>': path.resolve(__dirname, '<path>')
    //   }
    // }
    resolve: {
      extensions: ['.js', '.jsx', '.vue'],
      symlinks: false,
      alias: {
        "@": path.resolve(__dirname, './src'),
        'vue$': 'vue/dist/vue.esm-bundler.js',
        vue: path.resolve(__dirname, `./node_modules/vue`)
      }
    }
  },

  /* Webpack Configurations.

  Note: In vue/cli 3 or later the webpack config file is generated dynamically at runtime.
  It has been abstracted away. That is the reason you don't see a webpack config file.
  You can find the webpack config file here:
  <projectRoot>/node_modules/@vue/cli-service/webpack.config.js

  */
  devServer: {
    // If you want your server to be accessible externally from any ip, specify it with 0.0.0.0
    host: "0.0.0.0",
    port: "8080",
    hot: true,
    headers: {"Access-Control-Allow-Origin": "*"},

    devMiddleware: {
      /*
      Specify the ip address to WebPack Middleware package, DON"T confuse, it's something different
      from the main publicPath that defined above.
      */
      publicPath: "http://127.0.0.1:8080",
      /*
      When run 'npm run server' create a copy of 'index.html' file after format the source
      attributes of tags to refer to Webpack server local ip address that specified main publicPath,
      while when run 'npm run build' will create the 'index.html' file after format the source
      attributes to refer main publicPath '/static/dist/', which will served by backend server.
      */
      writeToDisk: (filePath) => filePath.endsWith("index.html"),
    },
    static: {
      //directory: path.resolve(__dirname, "static"),
      //staticOptions: {},
      // Don't be confused with `devMiddleware.publicPath`, it is `publicPath` for static directory.
      // publicPath: ['/static-public-path-one/', '/static-public-path-two/'],
      //publicPath: "/static-public-path/",
      //serveIndex: {}, (options for the `serveIndex` option).
      //serveIndex: true,
      watch: {
        ignored: "/node_modules/",
        usePolling: true,
      },
    },
    client: {
      /*
      To get protocol/hostname/port from browser:
      webSocketURL: 'auto://0.0.0.0:0/ws'
      */
      webSocketURL: {
        /*
        WebSocket is a computer communications protocol, providing full-duplex communication channels
        over a single TCP connection.

        Note: You need to config this option, otherwise the below error will occur in your browser
              console when trying to connect to Webpack from another Docker container:

              Error: WebSocket connection to 'ws://127.0.0.1:<port-number>/ws' failed
        */
        hostname: "0.0.0.0",
        pathname: "/ws",
        port: 8080,
      },
    },
  },
});

// function resolve (dir) {
//   return path.join(__dirname, '..', dir)
// }