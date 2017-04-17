var ExtractTextPlugin = require('extract-text-webpack-plugin');
module.exports = {
  entry: './app/upload.js',
  output: {
    filename: 'upload.js',
    path: '../src/collective/upload/browser/static',
    libraryTarget: 'umd',
    publicPath: '/++resource++collective.upload/',
    library: 'collective.upload'
  },
  externals: {
    jquery: 'jQuery'
  },
  resolve: {
    alias: {
      'canvas-to-blob': 'blueimp-canvas-to-blob/js/canvas-to-blob.js',
      'jquery-ui/ui/widget': 'blueimp-file-upload/js/vendor/jquery.ui.widget.js',
      'load-image': 'blueimp-load-image/js/load-image.js',
      'load-image-exif': 'blueimp-load-image/js/load-image-exif.js',
      'load-image-meta': 'blueimp-load-image/js/load-image-meta.js',
      'load-image-scale': 'blueimp-load-image/js/load-image-scale.js'
    }
  },
  module: {
    rules: [{
      test: /\.js$/,
      exclude: /(\/node_modules\/|test\.js$|\.spec\.js$)/,
      use: 'babel-loader',
    }, {
      test: /\.css$/,
      loader: ExtractTextPlugin.extract({
        use: [
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1
            }
          },
          'postcss-loader'
        ]
      })
    }, {
      test: /\.less$/,
      loader: ExtractTextPlugin.extract({
        fallback: 'style-loader',
        use: [
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1
            }
          },
          'postcss-loader',
          'less-loader'
        ]
      })
    }, {
      test: /.*\.(gif|png|jpe?g|svg)$/i,
      loaders: [
        'file-loader?name=[path][name].[ext]&context=app/',
        {
          loader: 'image-webpack-loader',
          query: {
            progressive: true,
            pngquant: {
              quality: '65-90',
              speed: 4
            },
            gifsicle: {
              interlaced: false
            },
            optipng: {
              optimizationLevel: 7
            }
          }
        }
      ]
    }, {
      test: /\.svg/,
      exclude: /node_modules/,
      use: 'svg-url-loader'
    }]
  },
  devtool: 'source-map',
  plugins: [
    new ExtractTextPlugin({
      filename: 'upload.css',
      disable: false,
      allChunks: true
    })
  ]
}
