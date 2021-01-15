const { STSClient, GetCallerIdentityCommand } = require("@aws-sdk/client-sts");

async function getCallerIdentity() {
  const client = new STSClient({ region: "us-east-1" });
  const command = new GetCallerIdentityCommand({});
  try {
    const results = await client.send(command);
    console.log(results.Arn);
  } catch (err) {
    console.error(err);
  }
}

getCallerIdentity();
