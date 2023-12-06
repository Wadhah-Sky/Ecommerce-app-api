const TIMINGFUNC_MAP = {
    "linear": t => t,
    "ease-in": t => t * t,
    "ease-out": t => t * (2 - t),
    "ease-in-out": t => (t < .5 ? 2 * t * t : -1 + (4 - 2 * t) * t)
};

function scrollTopSmooth(initY, duration = 300, timingName = "linear") {
    /**
     * Scroll from initY to 0
     * @param {number} initY - initial scroll Y
     * @param {number} duration - transition duration
     * @param {string} timingName - timing function name. Can be one of linear, ease-in, ease-out, ease-in-out
     */

    const timingFunc = TIMINGFUNC_MAP[timingName];
    let start = null;
    const step = (timestamp) => {
        start = start || timestamp;
        const progress = timestamp - start,
            // Growing from 0 to 1
            time = Math.min(1, ((timestamp - start) / duration));

        window.scrollTo(0, initY - (timingFunc(time) * initY));
        if (progress < duration) {
            window.requestAnimationFrame(step);
        }
    };

    window.requestAnimationFrame(step);
}

// Subscribe any element with [href="#"]
Array.from(document.querySelectorAll("[href='#']")).forEach(btn => {
    // Note: By marking a touch or wheel listener as passive, the developer is promising the handler
    //       won't call 'preventDefault()' to disable scrolling. This frees the browser up to respond to
    //       scrolling immediately without waiting for JavaScript, thus ensuring a reliably smooth scrolling
    //       experience for the user.
    btn.addEventListener("click", (e) => {
        e.preventDefault();
        scrollTopSmooth(window.scrollY, 300, "ease-in-out");
    }, {passive: true});
});

export {scrollTopSmooth};