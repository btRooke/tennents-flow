
const PORT = 8001;

export default class TennentsFlowSocket {
    constructor(tennentsFlow) {
        this.tennentsFlow = tennentsFlow;
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
            }
        });
        this.ws.onopen = () => this.sendInit();
    }

    handleInit = (initEvent) => {
        for (const pub of initEvent.pubs) {
            const lat = pub.coordinates[0];
            const long = pub.coordinates[1];
            console.log(pub);
            this.tennentsFlow.addPub(pub.name, lat, long);
        }
    }

    sendInit = () => {
        const initEvent = {
            type: "init"
        };

        this.ws.send(JSON.stringify(initEvent));
    }
}