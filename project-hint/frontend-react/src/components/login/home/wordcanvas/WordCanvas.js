import "d3-transition";
import { select } from "d3-selection";
import React, {useEffect, useReducer, useState} from "react";
import ReactWordcloud from "react-wordcloud";
import axios from "axios";
import randomColor from 'randomcolor';
import "tippy.js/dist/tippy.css";
import "tippy.js/animations/scale.css";

function getCallback(callback) {
  return function (word, event) {
    const isActive = callback !== "onWordMouseOut";
    const element = event.target;
    const text = select(element);
    text
      .on("click", () => {
        if (isActive) {
          window.location.assign(`/search/${word.text}`,
              "_blank");
        }
      })
        .transition()
        .attr("background", "white")
        .attr("text-decoration", isActive ? "underline" : "none");
  };
}

const callbacks = {
  // getWordColor: (word) => (word.value > 20 ? "var(--hana-green)" : "#9D968F"),
  getWordColor: (word) => randomColor({
    // count: 10,
    hue: 'random',//red, orange, yellow, green, blue, purple, pink and monochrome
    luminosity: 'bright',//bright, light or dark
    format: 'hex'
  }),
  // getWordColor:(word) =>
  //   (word.value >= 10 ?
  //     (word.value >= 20 ?
  //       (word.value >= 30 ? "blue" : "var(--hana-green)") : "skyblue") : "var(--pinkish-grey)"),
  getWordTooltip: (word) =>
    `"${word.text}" 키워드가 ${word.value}회 발견되었습니다.`,
  onWordClick: getCallback("onWordClick"),
  onWordMouseOut: getCallback("onWordMouseOut"),
  onWordMouseOver: getCallback("onWordMouseOver"),
};

const WordCanvas = () => {

  // useEffect(() => {
  //   setInterval(() => {
  //     handleChange();
  //   }, 3500);
  // });
  //
  // const [, forceUpdate] = useReducer(num => num + 1, 0);
  // function handleChange(){
  //   forceUpdate();
  // }

  const options = {
    enableTooltip: true,
    deterministic: false,
    fontFamily: "impact",
    padding: 2,
    fontSizes: [15, 70],
    fontStyle: "normal",
    fontWeight: "bold",
    rotations: 1,
    rotationAngles: [0, 90],
    scale: "sqrt",
    // scale: "log",
    // scale: "linear",
    spiral: "archimedean",
    transitionDuration: 1000,
    shuffle: true,
  };

  const [word, setWord] = useState({});
  useEffect(() => {
    axios
      .get(`http://127.0.0.1:5000/wordcloud`)
      // .get(`/wordcloud`)
      .then((res) => {
        console.log(res.data);
        setWord(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  return (
    <>
      <ReactWordcloud
        callbacks={callbacks}
        words={word}
        options={options}
        size={[610, 310]}
      />
    </>
  );
};

const rootElement = document.getElementById("root");
export default WordCanvas;
