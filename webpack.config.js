'use strict';
// var BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const NODE_ENV = process.env.NODE_ENV || 'development';

const webpack = require('webpack');
const path = require('path');

module.exports = {
    context: __dirname + '/frontend',
    entry: {
        puzzle: './geopuzzle',
        localization: './localization',
        // react: ['react', 'react-dom', 'redux', 'react-redux', 'react-google-maps', 'react-bootstrap'],
    },
    output: {
        path: path.resolve(__dirname, 'static'),
        filename: "js/[name].js",
    },
    resolve: {
        extensions: ['.js', '.jsx'],
    },
    watch: NODE_ENV == 'development',
    watchOptions: {
        aggregateTimeout: 100
    },
    target: 'node',
    devtool: 'cheap-inline-module-source-map',
    plugins: [
        new webpack.DefinePlugin({
            process: {
                env: {
                    NODE_ENV: JSON.stringify(NODE_ENV)
                }
            }
        }),
        // new BundleAnalyzerPlugin({
        //     analyzerMode: 'static'
        // })
    ],
    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                include: [
                    path.resolve(__dirname, "frontend")
                ],
                loader: 'babel-loader',
            },
            {
                test: /\.css$/,
                loader: 'style-loader!css-loader'
            }
        ]
    },
};