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
/*
  To install compression plugin:

  >> npm install compression-webpack-plugin --save-dev
 */
const CompressionPlugin = require('compression-webpack-plugin');
// The node:zlib module provides compression functionality implemented using Gzip, Deflate/Inflate, and Brotli.
// it's already folded withing node package.
const zlib = require("node:zlib");

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
      extensions: ['.js', '.jsx', '.vue', '.br'],
      symlinks: false,
      alias: {
        "@": path.resolve(__dirname, './src'),
        'vue$': 'vue/dist/vue.esm-bundler.js',
        vue: path.resolve(__dirname, `./node_modules/vue`)
      }
    },
    plugins: [
        // Use compression plugin to create minimized size of statics files, only for production.
        process.env.NODE_ENV === "production" ? new CompressionPlugin({
          /*
             Available options:

              1- test
              2- include
              3- exclude
              4- algorithm
              5- compressionOptions
              6- threshold
              7- minRatio
              8- filename
              9- deleteOriginalAssets

              Look at following link to know default and how to set options:

              https://github.com/webpack-contrib/compression-webpack-plugin
           */

          // Default for filename is "[path][base].gz"
          /*
            For example, we have following static >> assets/images/image.png?foo=bar#hash:

              [path] is replaced with the directories to the original asset, included trailing / (assets/images/).
              [file] is replaced with the path of original asset (assets/images/image.png).
              [base] is replaced with the base ([name] + [ext]) of the original asset (image.png).
              [name] is replaced with the name of the original asset (image).
              [ext] is replaced with the extension of the original asset, included . (.png).
              [query] is replaced with the query of the original asset, included ? (?foo=bar).
              [fragment] is replaced with the fragment (in the concept of URL it is called hash) of the original asset (#hash).
           */
          filename: '[path][base].br',
          // Brotli: is a  lossless data compression algorithm originally developed by Google,
          //         and offers compression superior to gzip.
          algorithm: 'brotliCompress',
          // set regex test to deal with files that pass it.
          // Note: if you want only to compress javascript files use the regex:
          //       /\.js(\?.*)?$/i
          test: /\.(js|css|html|svg)$/,
          compressionOptions: {
            params: {
              // Note: Brotli’s BROTLI_PARAM_QUALITY option is functionally equivalent to zlib’s level option
              //       that you are using in Nginx server.
              [zlib.constants.BROTLI_PARAM_QUALITY]: 11,
            },
          },
          // threshold means only assets bigger than this size are processed. In bytes. Default is 0
          threshold: 8192,
          /*
             minRatio is only assets that compress better than specified ratio are processed, Default is 0.8:

             (minRatio = Compressed Size / Original Size)

             Example: you have image.png file with 1024b size, compressed version of file has 768b size, so
                      minRatio equal 0.75. In other words assets will be processed when the:

                      Compressed Size / Original Size value

                      is less minRatio value.

                      Note: You can use 1 value to process assets that are smaller than the original.
                            Or use a value of 'Infinity' (no quotes) to process all assets even if they are larger
                            than the original size or their original size is 0 bytes (useful when you are pre-zipping
                            all assets for AWS cloud).
          */
          minRatio: Infinity,
          // Note: don't delete the original files because Nginx server can't handle <file-name>.extension.br and
          //       <file-name>.extension.gz without having <file-name>.extension version in folder, Nginx will send
          //       compressed files (of course if browser will send proper accept-encoding attribute in request
          //       (e.g. accept-encoding: gzip, deflate, br).
          // deleteOriginalAssets: true,
        }) : ""
    ]
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
    /*
      It seems like the compression-webpack-plugin only compresses files, but it doesn't automatically
      configure the dev server to serve the compressed files in place of the original file.

      You can manually setup a middleware via vue.config.js's devServer option (passed through to webpack-dev-server)
      to do this:

      1- Rewrite all .js requests that accept 'br' encoding to append .br to the original URL, which matches the filename
         setting given to compression-webpack-plugin. This effectively fetches the .br file compressed by the plugin.

      2- Set response headers to indicate the 'br' content encoding and application/javascript content type so that browsers
         could understand how to process the file.
     */
    setupMiddlewares(middlewares, devServer) {
      if (!devServer) {
        throw new Error('webpack-dev-server is not defined')
      }

      // middlewares.unshift({
      //   // In case you only compressed the all javascript files using Brotli algorithm.
      //   name: 'serve-brotli-js',
      //   // If you want to serve only .js files, use '*.js'
      //   path: '*.js',
      //   middleware: (req, res, next) => {
      //     if (req.get('Accept-Encoding')?.includes('br')) {
      //       req.url += '.br'
      //       res.set('Content-Encoding', 'br')
      //       res.set('Content-Type', 'application/javascript; charset=utf-8')
      //     }
      //     next()
      //   }
      // });

      return middlewares
    }
  },
});

// function resolve (dir) {
//   return path.join(__dirname, '..', dir)
// }