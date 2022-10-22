// import React, {useEffect, useRef} from "react";
//
// const useInterval = (callback, delay) => {
//
//     const savedCallback = useRef();
//
//     useEffect(() => {
//         savedCallback.current = callback;
//     }, [callback]);
//
//     useEffect(() => {
//         function tick() {
//             savedCallback.current();
//         }
//         if (delay !== null) {
//             let id = setInterval(tick, delay);
//             return () => clearInterval(id);
//         }
//     }, [delay]);
// }
//
// export default useInterval;

import React, {useEffect, useRef} from "react";

const useInterval = (callback, delay) => {

    const savedCallback = useRef(null);

    useEffect(() => {
        savedCallback.current = callback;
    }, [callback]);

    useEffect(() => {
        const executeCallback = () => {
            savedCallback.current();
        };

        const timerId = setInterval(executeCallback, delay);

        return () => clearInterval(timerId);

    }, []);
};

export default useInterval;
