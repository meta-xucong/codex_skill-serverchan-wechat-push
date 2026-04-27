---
name: serverchan-wechat-push
description: Send WeChat push notifications through ServerChan Turbo using a SendKey. Use when Codex needs to add, test, document, or call a WeChat notification or push feature in scripts, long-running tasks, monitors, automations, CI jobs, RPA workflows, or any workflow that should alert the user on completion, failure, approval-needed, or status changes.
---

# codex_skill: ServerChan WeChat Push

Use this skill whenever a task needs a lightweight WeChat notification through ServerChan Turbo.

## Quick Send

Prefer the bundled script for direct notifications:

```powershell
python "%USERPROFILE%\.codex\skills\serverchan-wechat-push\scripts\send_serverchan.py" --title "Task finished" --message "Please review the result."
```

The script reads the SendKey in this order:

1. `--sendkey`
2. `SCT_SENDKEY` environment variable
3. `%USERPROFILE%\.codex\secrets\serverchan_sendkey.txt`

Do not print the full SendKey in normal output.

## Message Design

Keep push messages short enough to act on from a phone.

Include:

- what happened
- project/task name
- status such as `done`, `blocked`, `failed`, or `needs review`
- the next action expected from the user
- a compact verification or error summary when useful

Use Markdown in `--message` when structure helps. Avoid dumping long logs into WeChat; include only the important lines and tell the user where to inspect the full result.

## Common Scenarios

Completion review:

```powershell
python "%USERPROFILE%\.codex\skills\serverchan-wechat-push\scripts\send_serverchan.py" --title "Task finished, review needed" --short "Codex result is ready" --message "The task has completed. Please return to the computer and review the result."
```

Blocked:

```powershell
python "%USERPROFILE%\.codex\skills\serverchan-wechat-push\scripts\send_serverchan.py" --title "Task blocked" --short "Manual action needed" --message "The task needs credentials, account access, external approval, or a product decision before it can continue."
```

Failure:

```powershell
python "%USERPROFILE%\.codex\skills\serverchan-wechat-push\scripts\send_serverchan.py" --title "Automation failed" --short "Check latest error" --message "The automation failed. Check the terminal or logs for the latest error."
```

Test without sending:

```powershell
python "%USERPROFILE%\.codex\skills\serverchan-wechat-push\scripts\send_serverchan.py" --title "Test" --message "This will not really send." --dry-run
```

## Integrating Into Code

For one-off shell/RPA/long-task integrations, call `scripts/send_serverchan.py` as a subprocess.

For application code, implement a small wrapper around:

```text
POST https://sctapi.ftqq.com/{SENDKEY}.send
```

Pass form fields:

- `title`: required
- `desp`: detailed content, Markdown supported
- `short`: optional card summary
- `noip`: optional, `1` hides caller IP
- `channel`: optional channel override
- `openid`: optional recipient override for supported channels

Read `references/serverchan-api.md` when adding a reusable integration, selecting channel values, or debugging ServerChan responses.

## Verification

After adding a push call, verify with either:

- `--dry-run` for message formatting
- one real send when the user has allowed test messages

Successful ServerChan responses usually contain `code: 0` and `data.error: SUCCESS`.
