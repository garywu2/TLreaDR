let config = {
  api: {
    protocol: "http",
    host: "192.168.0.24",
    port: 7082,
    prefix: "api"
  }
};

config.endpoint =
  config.api.protocol +
  "://" +
  config.api.host +
  ":" +
  config.api.port +
  "/" +
  config.api.prefix +
  "/";

module.exports = config;
