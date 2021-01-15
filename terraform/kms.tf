resource "aws_kms_key" "signing" {
  description              = "STS get-caller-identity assertion signing key"
  key_usage                = "SIGN_VERIFY"
  customer_master_key_spec = "RSA_4096"
  policy                   = data.aws_iam_policy_document.signing_key_policy.json
}

resource "aws_kms_alias" "signing" {
  name          = "alias/identity-assertion-signing"
  target_key_id = aws_kms_key.signing.key_id
}

data "aws_iam_policy_document" "signing_key_policy" {
  statement {
    actions   = ["kms:*"]
    resources = ["*"]

    principals {
      type = "AWS"
      identifiers = [
        "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root", # current account
      ]
    }
  }
}
