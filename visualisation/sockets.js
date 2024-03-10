
const PORT = 8001;

export default class TennentsFlowSocket {
    constructor(tennentsFlow) {
        this.tennentsFlow = tennentsFlow;
        this.id = null;
        this.initWS();
    }

    initWS = () => {
        this.ws = new WebSocket(`wss://${window.location.hostname}:${PORT}`)
        this.ws.addEventListener("message", ({ data }) => {
            const event = JSON.parse(data);

            switch (event.type) {
                case "init":
                    this.handleInit(event);
                    break;
                case "next_step":
                    this.handleNextStep(event);
                    break;
            }
        });
        this.ws.onopen = () => this.sendInit();
    }

    handleInit = (initEvent) => {
        this.id = initEvent.uuid;

        for (const pub of initEvent.pubs) {
            const lat = pub.location[0];
        const long = pub.location[1];
            console.log(pub);
            this.tennentsFlow.addPub(pub.name, lat, long, pub.size);
        }
    }

    handleNextStep = nextStepEvent => {

        const leaderBoard = [];

        for (const [pub1, moves] of Object.entries(nextStepEvent.data.agents)) {
            for (const [pub2, numPeople] of Object.entries(moves)) {
                this.tennentsFlow.moveActors(pub1, pub2, numPeople);
            }
        }

        for (const revenue of nextStepEvent.data.revenue) {
            for (const [pubName, amount] of Object.entries(revenue)) {
                this.tennentsFlow.displayRevenue(pubName, amount);
                leaderBoard.push({ pubName, revenue: amount });
            }
        }

        leaderBoard.sort((l1, l2) => l2.revenue - l1.revenue);

        const leaderboardElement = document.getElementById("leaderboard");
        leaderboardElement.innerHTML = "";

        leaderBoard.forEach(l => {
            const li = document.createElement("li");
            li.innerText = `${l.pubName} - £${l.revenue.toFixed(2)}`
            leaderboardElement.appendChild(li);
        });
    }

    sendInit = () => {
        const initEvent = {
            type: "init"
        };

        this.ws.send(JSON.stringify(initEvent));
    }

    sendNextStep = () => {
        const nextStepEvent = {
            type: "next_step",
            uuid: this.id
        }

        this.ws.send(JSON.stringify(nextStepEvent));
    }
}