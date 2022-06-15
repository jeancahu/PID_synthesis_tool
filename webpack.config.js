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
      'js/mathjax': {
        import: './js/mathjax.js',
      },
      'js/model_as_input': {
        import: './js/model_as_input.js',
      },
      'js/response_as_input': {
        import: './js/response_as_input.js',
      },
      'js/results': {
        import: './js/results.js',
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
