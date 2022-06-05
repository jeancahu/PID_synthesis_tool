const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    target: 'web',
    devtool: 'source-map',
    plugins: [new MiniCssExtractPlugin({
        filename: 'css/main_style.css',
    })],
    entry: {
        'js/main_style': {
            import: './js/index.js',
        },
    },
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, 'src/pidtuningtool/static/pidtuningtool/'),
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                enforce: "pre",
                use: ["source-map-loader"],
            },
            {
                test: /\.s?css/i,
                use: [MiniCssExtractPlugin.loader,
                      'css-loader',
                      'postcss-loader',
                      'sass-loader'],
            },
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/i,
                type: 'asset/resource',
            },
        ],
    },
};
