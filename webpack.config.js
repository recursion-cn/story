var webpack = require('webpack');
var commonsPlugin = new webpack.optimize.CommonsChunkPlugin('dep.js');

module.exports = {
    entry: {
        app: './assets/js/app.js',
        edit: './assets/js/edit.js',
        signup: './assets/js/signup.js',
        login: './assets/js/login.js',
        post: './assets/js/post.js'
    },
    output: {
        path: './assets/dist/js',
        filename: '[name].js'
    },

    module: {
        loaders: [
            {test: /\.js$/, exclude: /node_modules|bower_components/, loader: 'babel-loader'},
            {test: /\.less$/, loader: 'less'},
            //{test: /\.(woff|woff2)(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=application/font-woff'},
            //{test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=application/octet-stream'},
            //{test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, loader: 'file'},
            //{test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=image/svg+xml'}
        ]
    },

    plugins: [commonsPlugin]
};

