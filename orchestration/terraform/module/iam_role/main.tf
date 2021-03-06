resource "aws_iam_policy_attachment" "attachment" {
  name = "${var.role_name}Attachment"
  policy_arn = "${aws_iam_policy.policy.arn}"
  roles = [
    "${aws_iam_role.role.name}"
  ]
}

resource "aws_iam_role" "role" {
  name = "${var.role_name}Role"
  path = "${var.path}"
  assume_role_policy = "${file("${var.assume_role_policy_json}")}"
}

resource "aws_iam_policy" "policy" {
  name = "${var.role_name}Policy"
  path = "${var.path}"
  policy = "${var.policy}"
}
