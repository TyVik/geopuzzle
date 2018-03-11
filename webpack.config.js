'use strict';
var BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const NODE_ENV = process.env.NODE_ENV || 'development';

const webpack = require('webpack');
const path = require('path');
const SentryCliPlugin = require('@sentry/webpack-plugin');

function _isVendor(module) {
    return module.context && module.context.indexOf('node_modules') !== -1;
}

function _isCSS(module) {
    return module.context && /\.css$/.test(module.context);
}

module.exports = (env) => {
    env = env || {};
    const config = {
        context: __dirname + '/frontend',
        entry: {
            quiz: './quiz',
            puzzle: './puzzle',
            localization: './localization',
            tree: './tree',
            react: ['react', 'react-dom', 'redux', 'react-redux'],
        },
        output: {
            path: path.resolve(__dirname, 'static'),
            filename: "js/[name].js",
            sourceMapFilename: "js/[name].map",
        },
        resolve: {
            extensions: ['.js', '.jsx'],
        },
        watch: NODE_ENV == 'development',
        watchOptions: {
            aggregateTimeout: 100
        },
        devtool: 'source-map',
        // devtool: 'cheap-inline-module-source-map',
        plugins: [
            new webpack.DefinePlugin({
                process: {
                    env: {
                        NODE_ENV: JSON.stringify(NODE_ENV)
                    }
                }
            }),
            new webpack.optimize.CommonsChunkPlugin({
                name: 'react',
                chunks: ['puzzle', 'quiz'],
                minChunks: Infinity,
            }),
            new webpack.optimize.CommonsChunkPlugin({
                name: 'vendor',
                chunks: ['puzzle', 'quiz'],
                minChunks: function (module) {
                    return _isVendor(module) && !_isCSS(module);
                }
            }),
        ],
        module: {
            rules: [
                {
                    test: /\.jsx?$/,
                    exclude: /node_modules/,
                    use: [
                        {loader: 'babel-loader'}
                    ]
                },
                {
                    test: /\.css$/,
                    exclude: /node_modules/,
                    use: [
                        {
                            loader: 'style-loader'
                        },
                        {
                            loader: 'css-loader',
                            options: {
                                importLoaders: 1
                            }
                        },
                    ]
                }

            ]
        }
    };

    if (NODE_ENV == 'production') {
        config.plugins.push(
            new SentryCliPlugin({
                include: './static/js',
                configFile: 'sentry.properties',
                ignore: ['node_modules', 'webpack.config.js'],
            })
        );
        config.plugins.push(
            new BundleAnalyzerPlugin({
                analyzerMode: 'static'
            })
        );
    }
    return config;
}
    ;
