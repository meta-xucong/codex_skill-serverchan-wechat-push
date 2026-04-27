# ServerChan Turbo API Notes

## Endpoint

```text
POST https://sctapi.ftqq.com/{SENDKEY}.send
```

Use `application/x-www-form-urlencoded` form fields. GET also works for simple tests, but POST is preferred because Chinese text and longer Markdown content are easier to handle.

## Parameters

`title`
: Required message title.

`desp`
: Optional detailed content. Markdown is supported.

`short`
: Optional card summary. Use this for a compact phone notification line.

`noip`
: Optional. Use `1` to hide the caller IP when supported.

`channel`
: Optional. Overrides the default channel configured on the Server酱 website for this send. Multiple channel values can be joined with `|`.

`openid`
: Optional. Supported only by some channels, such as test account and WeCom app message. Use the channel-specific recipient identifier.

## Common Channel Values

- `98`: official Android beta client
- `66`: WeCom app message
- `1`: WeCom group robot
- `2`: DingTalk robot
- `3`: Feishu/Lark robot
- `8`: Bark iOS
- `0`: test account
- `88`: custom webhook
- `18`: PushDeer
- `9`: Fangtang service account

## Response

Success normally looks like:

```json
{
  "code": 0,
  "message": "",
  "data": {
    "pushid": "34297783",
    "readkey": "SCT...",
    "error": "SUCCESS",
    "errno": 0
  }
}
```

Treat `code == 0` as success. Keep `pushid` in logs when useful for debugging.

## Message Template

```markdown
# <title>

Project: `<project>`

Status: `<done|blocked|failed|needs review>`

Summary: <short actionable summary>

Latest verification: <test/check result>

Next action: <what the user should do>
```
