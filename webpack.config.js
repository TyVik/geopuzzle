'use strict';
const NODE_ENV = process.env.NODE_ENV || 'development';

const webpack = require('webpack');
const path = require('path');


module.exports = {
    entry: './frontend/puzzle.js',
    output: {
        path: path.resolve(__dirname, 'static'),
        filename: 'puzzle.js'
    },
    resolve: {
        extensions: ['.js', '.jsx', '.scss'],
    },
    watch: NODE_ENV == 'development',
    watchOptions: {
        aggregateTimeout: 100
    },
    target: 'node',
    devtool: 'cheap-inline-module-source-map',
    plugins: [
        new webpack.NoEmitOnErrorsPlugin(),
        new webpack.DefinePlugin({NODE_ENV: JSON.stringify(NODE_ENV)})
    ],
    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                loader: 'babel-loader?presets[]=es2015',
                include: [
                    path.relative(__dirname, "/frontend")
                ],
            }
        ]
    },
};