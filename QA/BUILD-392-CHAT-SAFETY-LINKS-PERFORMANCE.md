# NgelX Build 392 – Chat Safety, Links and Performance

## Protected Build 391 behaviors
- Build/version screen remains available.
- Blocking confirmation remains in place.
- A blocked private conversation keeps old history while disabling new message/call actions.
- Reopening a private conversation keeps its messages.
- Message-content search and immediate indexing of new messages remain available.
- Media gallery, video playback and voice-message archive/playback remain available.

## Build 392 fixes
1. Blocking severs follow/follower/friend relationships on both accounts; unblocking does not restore them automatically.
2. Other-user profiles expose Share + three-dot moderation actions (block/unblock/report), including blocked/inaccessible profile states.
3. Profile sharing offers NgelX-internal sharing and the system share sheet.
4. Group entry warns when a blocked member is present; blocked members' messages are hidden until explicitly revealed.
5. Private system events authored by the current user render as “Sen …” to prevent actor confusion.
6. Private chat search can match the other participant's display name as well as message text.
7. Plain-text HTTP(S) links are indexed in the Links archive, even for old messages that do not have a stored linkUrl.
8. Chat links are visually identified, tappable, and open externally; concatenated links are separated before send.
9. Deleting a private message leaves a tombstone instead of removing the document.
10. File/document sending and the Files tab are removed from private-chat UI.
11. Pinning is removed from private chat; group pinning remains.
12. Disappearing private messages show a timer indicator.
13. Private chat initial/live history is bounded to 70 messages; media/search queries are also bounded more tightly.

## Manual regression checks
- Block → follow/follower/friend relation disappears.
- Unblock → relation stays removed.
- Send a URL → tap it and verify it appears under Links.
- Delete a private message → tombstone remains for both participants.
- Enable 24h disappearing messages → newly sent message shows the timer marker.
- Open a group containing a blocked member → warning appears; that member's message is censored until tapped.
- Search the private chat for the other person's display name.
- Scroll/send/reopen a long private chat and verify responsiveness.
