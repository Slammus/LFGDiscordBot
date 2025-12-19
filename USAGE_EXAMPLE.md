# Usage Example

This document shows how the LFG Discord Bot works in practice.

## Starting a Session

A user types the following command:
```
/lfg game:"Valorant" min_players:5 max_players:5
```

The bot creates an interactive message that looks like this:

---

### 🎮 Looking for Group Session

Click the buttons below to join games or add new ones!

**Valorant (0/5-5) ⏳ Waiting**
No players yet

---

[Join Valorant] [➕ Add Game]

---

## Users Join the Game

Three users click "Join Valorant":

---

### 🎮 Looking for Group Session

Click the buttons below to join games or add new ones!

**Valorant (3/5-5) ⏳ Waiting**
@User1, @User2, @User3

---

[Join Valorant] [➕ Add Game]

---

## Adding Another Game

User4 clicks "➕ Add Game" and fills in the modal:
- Game Name: Among Us
- Minimum Players: 4
- Maximum Players: 10

The message updates:

---

### 🎮 Looking for Group Session

Click the buttons below to join games or add new ones!

**Valorant (3/5-5) ⏳ Waiting**
@User1, @User2, @User3

**Among Us (0/4-10) ⏳ Waiting**
No players yet

---

[Join Valorant] [Join Among Us] [➕ Add Game]

---

## Minimum Players Reached

Four more users join Among Us (Users 4, 5, 6, 7):

The bot sends a notification in the channel:
```
🎮 Among Us has reached the minimum number of players! (4/4)
Players: @User4 @User5 @User6 @User7
```

The message updates to show the ready status:

---

### 🎮 Looking for Group Session

Click the buttons below to join games or add new ones!

**Valorant (3/5-5) ⏳ Waiting**
@User1, @User2, @User3

**Among Us (4/4-10) ✅ Ready!**
@User4, @User5, @User6, @User7

---

[Join Valorant] [Join Among Us] [➕ Add Game]

---

## Ending a Session

The session creator or a moderator types:
```
/endlfg
```

The bot confirms the session has ended.

## Features Demonstrated

1. **Interactive Buttons**: Users can join/leave games with one click
2. **Real-time Updates**: The message automatically updates as players join
3. **Multiple Games**: Sessions can have multiple games simultaneously
4. **Dynamic Addition**: Anyone can add new games during the session
5. **Smart Notifications**: Bot announces when games are ready to start
6. **Visual Status**: Clear indicators show which games are ready
7. **Player Lists**: See exactly who wants to play each game
