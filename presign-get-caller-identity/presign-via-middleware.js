const fs = require("fs");
const { STSClient, GetCallerIdentityCommand } = require("@aws-sdk/client-sts");
const { awsAuthMiddlewareOptions } = require("@aws-sdk/middleware-signing");

const ERROR_CODE = "SIGNING_COMPLETED_ABORTING";

const logMiddleware = (next, context) => async (args) => {
  const err = new Error(ERROR_CODE);
  err.request = args.request;
  throw err;
};

const client = new STSClient({ region: "us-east-1" });
client.middlewareStack.addRelativeTo(logMiddleware, {
  relation: "after",
  toMiddleware: awsAuthMiddlewareOptions.name,
});

async function getCallerIdentitySignedRequest() {
  const command = new GetCallerIdentityCommand();
  try {
    const results = await client.send(command);
  } catch (err) {
    if (err.message == ERROR_CODE) {
      return err.request;
    } else {
      throw err;
    }
  }
}

const storeData = (data, path) => {
  try {
    fs.writeFileSync(path, JSON.stringify(data));
  } catch (err) {
    console.error(err);
  }
};

(async () => {
  const signedRequest = await getCallerIdentitySignedRequest();
  const transformed = {
    url: `https://${signedRequest.hostname}`,
    headers: signedRequest.headers,
    body: signedRequest.body,
  };
  storeData(transformed, "../request.json");
})();
