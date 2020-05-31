const path = require("path");
const process = require("process");
const SriPlugin = require("webpack-subresource-integrity");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const BundleTracker = require("webpack-bundle-tracker");
const ForkTsCheckerWebpackPlugin = require("fork-ts-checker-webpack-plugin");

module.exports = {
  mode: process.env.NODE_ENV || "development",
  entry: {
    browser: "./virtualbarcamp/browser/index.tsx",
    accounts: "./virtualbarcamp/accounts/browser/index.ts",
  },
  output: {
    path: path.resolve(__dirname, "build"),
    publicPath: process.env.NODE_ENV !== "production" ? "http://localhost:3000/" : undefined,
    chunkFilename: "[name].[chunkhash].js",
    filename: process.env.NODE_ENV === "development" ? "[name].[hash].js" : "[name].[chunkhash].js",
    crossOriginLoading: "anonymous",
  },
  plugins: [
    new SriPlugin({
      hashFuncNames: ["sha256"],
    }),
    new MiniCssExtractPlugin({
      filename: "[name].[chunkhash].css",
      chunkFilename: "[id].css",
    }),
    new BundleTracker({
      filename: "manifest.json",
      integrity: true,
    }),
    new ForkTsCheckerWebpackPlugin(),
  ],
  resolve: {
    extensions: [".ts", ".tsx", ".js"],
  },
  module: {
    rules: [
      { test: /\.tsx?$/, loader: "ts-loader", options: { transpileOnly: true } },
      {
        test: /\.css$/,
        use: [
          process.env.NODE_ENV !== "production" ? "style-loader" : MiniCssExtractPlugin.loader,
          "css-loader",
        ],
      },
      {
        test: /\.scss$/,
        use: [
          process.env.NODE_ENV !== "production" ? "style-loader" : MiniCssExtractPlugin.loader,
          "css-loader",
          "sass-loader",
        ],
      },
      {
        test: /\.(png|svg|jpg|gif|woff|woff2|eot|ttf|otf)$/,
        use: ["file-loader"],
      },
    ],
  },
  devtool: process.env.NODE_ENV === "production" ? "source-map" : "eval-source-map",
  devServer: {
    port: 3000,
    hot: true,
    allowedHosts: ["localhost", "ui"],
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET",
    },
  },
};
