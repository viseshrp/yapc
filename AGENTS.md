# Repository instructions

## Scheduled automation ownership and recovery

The user's October 28, 2026 instruction takes precedence over earlier
clean-worktree or original-checkout-only automation rules. Dirty working
directories never block scheduled jobs. Automations must commit and push their
own validated changes without committing or rearranging pre-existing work.

- Record the original branch, HEAD, index entries, and owner file hashes.
  Preserve staged, unstaged, untracked, overlapping, private, and live state.
- Use exact owned paths or hunks only. A path that already contains owner edits
  is not wholly owned by the job. If existing staging, overlap, another branch,
  divergence, or concurrent publication complicates separation, automatically
  use an isolated checkout at the verified remote destination and run the job
  there. Its registered output paths are relative to that checkout. Do not
  require the original checkout to be clean or synchronized before proceeding.
- Never stash, reset, clean, move owner files out of the way, stage everything,
  or commit pre-existing work to satisfy a preflight check. Review and validate
  only the job's complete delta, commit it, and push the configured destination.
- Recover a rejected push by fetching the destination in an isolated checkout,
  reapplying only the owned delta, reconciling concurrent append-only changes,
  rerunning affected checks, and retrying normally. Never force-push or alter
  owner history. Verify the published checkout and live remote SHA, required
  CI, and original owner-state preservation; failed attempts may be retried.
- Diagnose and fix recoverable failures within the job's existing scope, then
  rerun validation and finish publication. A missing credential or unavailable
  source fact cannot be invented: report that precise external prerequisite
  and finish independent valid work. Preserve source permissions, privacy,
  validation, no-execution rules, and no-change behavior. Record reusable
  symptom/cause/fix/verification evidence in the existing job continuity files.
