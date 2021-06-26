'use strict';
const webpack = require('webpack');
const path = require('path');


module.exports = (env, argv) => {
  const NODE_ENV = process.env.NODE_ENV || 'development';

  return {
    context: __dirname + '/frontend',
    entry: {
      games: './games',
      workshop: './workshop',
      profile: './profile',
      index_games: './index_games',
    },
    output: {
      path: path.resolve(__dirname, 'static', 'js'),
      filename: "[name].js",
      sourceMapFilename: "[name].map",
    },
    resolve: {
      extensions: ['.js', '.jsx'],
    },
    watchOptions: {
      aggregateTimeout: 100
    },
    devtool: 'source-map',
    plugins: [
      new webpack.DefinePlugin({
        process: {
          env: {
            NODE_ENV: JSON.stringify(NODE_ENV)
          }
        }
      }),
    ],
      module: {
        rules: [{
          test: /\.jsx?$/,
            exclude: /node_modules/,
            use: ['babel-loader']
          }, {
            test: /\.css$/,
            exclude: /node_modules/,
            use: ['style-loader', 'css-loader']
        }]
      },
      optimization: {
        splitChunks: {
          cacheGroups: {
            commons: {
              test: /node_modules\/(?!html2canvas)/,
              chunks: 'initial',
              name: 'common',
              enforce: true,
            },
            components: {
              test: /components/,
              chunks: 'initial',
              name: 'components',
              enforce: true,
            },
          },
        },
      },
    };
};
