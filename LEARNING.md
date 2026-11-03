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
- Evidence links / next step: [Issue #3](https://github.com/ssp344/my-app-studio/issues/3). Full APP-002 and normal checks passed: 98 foundation, 14 cumulative contracts and 2 Chromium tests. [PR #4](https://github.com/ssp344/my-app-studio/pull/4) merged; issue #3 closed and both main CI jobs passed.

## APP-003

- Prediction: After AI scenarios, learner predicted blocking members: “it should block becuase only /admin can access the data and all the info not the user”. AI clarified that the admin role grants access, not typing the address.
- Check interpretation: Pending. AI showed member 403, admin 200, and downgraded-member 403 for direct API requests. Learner requested a separate admin sign-in flow rather than independently interpreting that test.
- Browser observation: As shivadmin: “i see admin only info whats the store name sample 3 book and also see return to yout dashboard”. As regular test account: “i tried to login as test and access required. this is perfect”.
- Keep decision: “i like it because this is an simple flow for admin and the usert”.
- Review: Learner reviewed the summary and replied “this is good” before publication. AI reviewed permission enforcement, existing-session role changes, signup restrictions, and desktop/mobile admin layouts.
- Help/gaps: AI implemented routes, templates and tests. Learner requested a distinct admin sign-in page and chose shivadmin; learner entered the password privately, then AI promoted the local account through the trusted CLI. No shared passkey or public role assignment was added. The prepared anonymous /admin redirect to /login remains; /login links to /admin/login. A mistaken /dashboard/admin visit was distinguished from a permission denial. Independent direct-request interpretation remains pending.
- Evidence links / next step: [Issue #5](https://github.com/ssp344/my-app-studio/issues/5). Full normal checks passed: 99 foundation, 18 cumulative contracts, 2 Chromium tests. [PR #6](https://github.com/ssp344/my-app-studio/pull/6) merged; issue #5 closed. Verify latest main CI before submitting.
