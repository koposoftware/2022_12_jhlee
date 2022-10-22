import React, {useState} from "react";
// import "./styles.css";
import Lottie from "react-lottie";
import animationData from "./lotties/research.json";
import animationData2 from "./lotties/analysis.json";

const LottieButton = () => {

    const defaultOptions = {
        loop: true,
        autoplay: false,
        animationData: animationData2,
        rendererSettings: {
            preserveAspectRatio: "xMidYMid slice"
        }
    };

    return (
        // <div onMouseEnter={() => this.lottie && this.lottie.animation.play()}
        //      onMouseLeave={() => this.lottie && this.lottie.animation.pause()}>
        <div>
            <Lottie
                options={defaultOptions}
                height={290}
                width={300}
                // ref={(ref) => this.lottie = ref}
            />
        </div>
    );
}

export default LottieButton