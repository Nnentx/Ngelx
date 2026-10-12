# Build443 device follow-up — 46552.mp4, 12 October 2026

Observed source: 86.335-second user device recording. Settings shows v1.0.218 / Build443. Account identifiers and personal images are intentionally omitted from this note.

Confirmed: sign-in proceeds to feed in the first seconds; the feed spinner then gives way to content. This recording does not establish a persistent startup hang. Create, inbox, profile and multiple settings routes open. No two-device media/calling acceptance is demonstrated.

Capture issue reported by user: enabling allowProfileCapture does not immediately remove the capture restriction; closing and reopening the application allows capture. In the recording, a black capture interval appears while the account-switch page was being visited, outside visible profile content. Diagnose native lease ownership/visibility and preference propagation; do not present restarting as the permanent fix.

Latest requested behavior supersedes Build443 defaults: capture blocking OFF by default. Label the switch as “Profil ekran kaydını ve görüntüsünü engelle”. Turning blocking ON protects the profile; OFF releases it immediately without restarting. Keep the owner preference persistent, avoid blocking unrelated routes/application startup, and test both profiles/accounts, nested media, return navigation, account changes and background/reopen. Changes are requested, not yet implemented in a new APK.

Remaining English presentation gaps visible in this recording: feed preparing/save labels and timestamps; Create live tab; profile/delete confirmation and success messages; account-switch header/current-account/switch/add labels; privacy subcategory/download preference; message-permission/request/invite/read-receipt descriptions; friends tabs/search/count/activity labels; suspicious-login/session heading. Existing notification system-event descriptions remain Turkish. Render structured event descriptions in the viewer locale while preserving names, group titles, user messages and historic stored records.

Post deletion: confirmation and success messages are visible, while the subsequent profile grid still shows three cards. This alone does not prove server deletion failure; verify the deleted ID and refresh/removal behavior with a controlled test. Do not claim deletion acceptance from a toast.

Deliver these findings together with the capture-default/live-update fix in the next consolidated package. Build443 remains the installed diagnostic candidate; no new build is claimed by this note.
