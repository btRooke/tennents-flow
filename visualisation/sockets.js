
const PORT = 8001;

export default class TennentsFlowSocket {
    constructor(tennentsFlow) {
        this.tennentsFlow = tennentsFlow;
        this.id = null;
        this.initWS();
    }

    initWS = () => {
        this.ws = new WebSocket(`ws://${window.location.hostname}:${PORT}`)
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
        for (const pub of initEvent.pubs) {
            const lat = pub.location[0];
            const long = pub.location[1];
            this.tennentsFlow.addPub(pub.name, lat, long);
        }
        this.id = initEvent.uuid;
    }

    handleNextStep = nextStepEvent => {
        for (const [pub1, moves] of Object.entries(nextStepEvent.data.agents)) {
            for (const [pub2, numPeople] of Object.entries(moves)) {
                this.tennentsFlow.moveActors(pub1, pub2, numPeople);
            }
        }

        for (const revenue of nextStepEvent.data.revenue) {
            for (const [pubName, amount] of Object.entries(revenue)) {
                this.tennentsFlow.displayRevenue(pubName, amount);
            }
        }
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