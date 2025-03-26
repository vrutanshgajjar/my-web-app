const express = require("express");
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json()); 

let users = [
    { id: 1, name: "Vrutansh Gajjar", email: "vrutansh@gmail.com" },
    { id: 2, name: "Tarj Baxi", email: "tarj@gmail.com" },
    { id: 3, name: "Anmol", email: "anmol@gmail.com" },
    { id: 4, name: "Jay Patel", email: "jaypatel@gmail.com" },
    { id: 5, name: "Parth", email: "parth@gmail.com" }
];

app.get("/users", (req, res) => {
    res.json(users);
});

app.get("/users/:id", (req, res) => {
    const id = parseInt(req.params.id);
    const user = users.find(user => user.id === id);

    if (user) {
        res.json(user);
    } else {
        res.status(404).send("User not found");
    }
});

app.post("/users", (req, res) => {
    const newUser = {
        id: users.length + 1,  
        name: req.body.name,
        email: req.body.email
    };

    users.push(newUser);
    res.status(201).json(newUser);
});

app.put("/users/:id", (req, res) => {
    const user = users.find(u => u.id === parseInt(req.params.id));

    if (!user) return res.status(404).json({ message: "User not found" });

    user.name = req.body.name || user.name;
    user.email = req.body.email || user.email;

    res.json(user);
});

app.delete("/users/:id", (req, res) => {
    users = users.filter(u => u.id !== parseInt(req.params.id));
    res.json({ message: "User deleted" });
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
