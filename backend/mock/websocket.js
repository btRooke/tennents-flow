
const ws = new WebSocket("ws://localhost:8001");

function sendHello() {
    const event = {
        type: "hello",
    };

    ws.send(JSON.stringify(event));
}

window.addEventListener("DOMContentLoaded", () => {
    ws.addEventListener("message", ({ data }) => {
        const event = JSON.parse(data);

        switch (event.type) {
            case "hello":
                console.log("hello");
                break;
        }
    });
});

