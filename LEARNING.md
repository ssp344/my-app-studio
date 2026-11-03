# Conversation evidence

AI-drafted task summary, not a transcript or grade. It may be public. Use actual
short words or labeled paraphrases; disclose help and leave missing responses
pending. The learner reviews, corrects or removes new excerpts before commit/push.
Accuracy approval is not proof of understanding. Label simulated trials explicitly.

**Available conversation context:** This setup and bookstore planning chat.

## APP-001

- Prediction: Pending.
- Check interpretation: Selected “Broken link” from two AI-provided scenarios for the Browse books check. An independent explanation was not supplied.
- Browser observation: Starter: “i see one simple blank structure and see begin here and see the next step arrow”. After trying Browse books: “yes when i click it bring me little bottom where all the book is listed”.
- Keep decision: “Yes i like it and i love how simple and easy to quick look”.
- Review: AI reviewed the changed source, desktop and narrow screenshots, keyboard/navigation checks, and full APP-001 results. Learner reviewed the summary and replied “looks good” before publication.
- Help/gaps: Learner chose a bookstore open to everyone, named it “Shiv's Book Store!”, and requested simple book cards with names, prices, and short descriptions. AI suggested the promise, Everyperson personality, sample books, colors, and implementation. Prediction remains pending after prompts and a hint; approval was not treated as a prediction. Learner reviewed the summary before publication.
- Evidence links / next step: [Issue #1](https://github.com/ssp344/my-app-studio/issues/1). Full APP-001 checks passed; summary reviewed and published. [PR #2](https://github.com/ssp344/my-app-studio/pull/2) merged; issue closed and both main CI jobs passed. Prediction remains pending.

## APP-002

- Prediction: Selected redirecting an anonymous dashboard visitor to login from AI-provided scenarios. Reason: “because security reason need to log in to see private dashboard that no one can access”. Post-login prediction not separately supplied.
- Check interpretation: Pending. Learner initially confused reusing an old session cookie with logging in again using credentials. AI explained that credentials can be used for a new login but logout must revoke the old session; independent copied-cookie interpretation remains incomplete.
- Browser observation: After signup/login and logout, learner reopened the dashboard and reported “log in page”.
- Keep decision: “i like this because no one can access after logout”. This describes the logged-out session; a fresh valid login remains allowed.
- Review: Learner reviewed the summary and replied “looks good” before publication. AI reviewed code, security helper use, desktop/mobile signup rendering and full cumulative checks.
- Help/gaps: AI implemented forms/API routes, reused prepared security helpers and ran tests. AI supplied scenarios and explained session revocation. Missing interpretation stays pending. Learner requested shorter passwords; the prepared 15–128-character contract was retained after explanation.
- Evidence links / next step: [Issue #3](https://github.com/ssp344/my-app-studio/issues/3). Full APP-002 and normal checks passed: 98 foundation, 14 cumulative contracts and 2 Chromium tests. Publish reviewed work and verify PR CI before the merge decision.

## APP-003

- Prediction: Pending.
- Check interpretation: Pending.
- Browser observation: Pending.
- Keep decision: Pending.
- Review: Pending.
- Help/gaps: Pending.
- Evidence links / next step: Keep APP-002 before agreeing this lesson.
