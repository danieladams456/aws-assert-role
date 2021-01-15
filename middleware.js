const { STSClient, GetCallerIdentityCommand } = require("@aws-sdk/client-sts");
const { awsAuthMiddlewareOptions } = require("@aws-sdk/middleware-signing");

const logMiddleware = (next, context) => async (args) => {
  console.log(args.request);
  args.request.headers["x-amz-meta-foo"] = "bar";
  const result = next(args);
  // result.response contains data returned from next middleware.
  return result;
};

const client = new STSClient({ region: "us-east-1" });
client.middlewareStack.addRelativeTo(logMiddleware, {
  relation: "after",
  toMiddleware: awsAuthMiddlewareOptions.name,
});

async function getCallerIdentity() {
  const command = new GetCallerIdentityCommand({});
  try {
    const results = await client.send(command);
    console.log(results.Arn);
  } catch (err) {
    console.error(err);
  }
}
getCallerIdentity();
