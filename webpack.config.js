'use strict';
const webpack = require('webpack');
const path = require('path');
const SentryCliPlugin = require('@sentry/webpack-plugin');


module.exports = (env, argv) => {
    const NODE_ENV = process.env.NODE_ENV || 'development';

    const config = {
        context: __dirname + '/frontend',
        entry: {
            quiz: './quiz',
            puzzle: './puzzle',
            localization: './localization',
        },
        output: {
            path: path.resolve(__dirname, 'static', 'js'),
            filename: "[name].js",
            sourceMapFilename: "[name].map",
        },
        resolve: {
            extensions: ['.js', '.jsx'],
        },
        watch: argv.mode === 'development',
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
            })
        ],
        module: {
            rules: [{
                test: /\.jsx?$/,
                exclude: /node_modules/,
                use: [
                    {loader: 'babel-loader'}
                ]
            }, {
                test: /\.css$/,
                exclude: /node_modules/,
                use: [
                    {loader: 'style-loader'},
                    {loader: 'css-loader', options: {importLoaders: 1}},
                ]
            }]
        },
        optimization: {
            splitChunks: {
                cacheGroups: {
                    commons: {
                        test: /node_modules/,
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

/*
    if (NODE_ENV === 'production') {
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
*/
    return config;
};