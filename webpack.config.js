'use strict';
const webpack = require('webpack');
const path = require('path');
const SentryCliPlugin = require('@sentry/webpack-plugin');
const GitRevisionPlugin = require('git-revision-webpack-plugin');
const gitRevisionPlugin = new GitRevisionPlugin();


module.exports = (env, argv) => {
    const NODE_ENV = process.env.NODE_ENV || 'development';

    return {
        context: __dirname + '/frontend',
        entry: {
            games: './games',
            localization: './localization',
            editor: './editor',
            workshop: './workshop',
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
            }),
            new SentryCliPlugin({
                release: gitRevisionPlugin.version(),
                include: './static/js/',
                ignore: ['node_modules', 'webpack.config.js']
            })
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
};