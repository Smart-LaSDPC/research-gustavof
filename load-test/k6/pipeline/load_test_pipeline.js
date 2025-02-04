// k6 run load_test_pipeline.js
import { sleep } from 'k6';
import http from 'k6/http';
import { check } from 'k6';

// Distribution types
const DISTRIBUTIONS = {
    NORMAL: 'normal',
    POISSON: 'poisson',
    UNIFORM: 'uniform',
    EXPONENTIAL: 'exponential',
};

// Simple normal distribution approximation using Box-Muller transform
function normalDistribution(mean, stddev) {
    let u1 = Math.random();
    let u2 = Math.random();
    let z1 = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
    return mean + stddev * z1;
}

// Poisson distribution approximation using the inverse transform sampling method
function poissonDistribution(lambda) {
    let L = Math.exp(-lambda);
    let k = 0;
    let p = 1;
    do {
        k++;
        p *= Math.random();
    } while (p > L);
    return k - 1;
}

// Uniform distribution
function uniformDistribution(min, max) {
    return min + Math.random() * (max - min);
}

// Exponential distribution approximation
function exponentialDistribution(lambda) {
    return -Math.log(1 - Math.random()) / lambda;
}

// Sleep times for different distributions
function getWaitTime(distribution, params) {
    switch (distribution) {
        case DISTRIBUTIONS.NORMAL:
            return Math.abs(normalDistribution(params.mean, params.stddev));
        case DISTRIBUTIONS.POISSON:
            return poissonDistribution(params.lambda);
        case DISTRIBUTIONS.UNIFORM:
            return uniformDistribution(params.min, params.max);
        case DISTRIBUTIONS.EXPONENTIAL:
            return exponentialDistribution(params.lambda);
        default:
            return 1; // Default wait time if no distribution is specified
    }
}

// Test pipeline configurations for all distributions
const testPipeline = [
    { vus: 250, duration: '10m', distribution: DISTRIBUTIONS.NORMAL, mean: 1, stddev: 0.2 },
    { vus: 250, duration: '10m', distribution: DISTRIBUTIONS.UNIFORM, min: 0.5, max: 1.5 },


];

// Select the test based on the environment variable ITERATION_INDEX
const iterationIndex = __ENV.ITERATION_INDEX || 0;
const config = testPipeline[iterationIndex % testPipeline.length];

// Set k6 options dynamically based on the selected test
export let options = {
    vus: config.vus,
    duration: config.duration,
};

export default function () {
    const wait = getWaitTime(config.distribution, {
        mean: config.mean || 1,               // Default values for NORMAL
        stddev: config.stddev || 0.2,
        lambda: config.lambda || 1,           // Default values for POISSON and EXPONENTIAL
        min: config.min || 0.5,               // Default values for UNIFORM
        max: config.max || 1.5,
    });

    sleep(wait);

    // const res = http.get('http://localhost:8080/iot');
    const res = http.get('http://iot-api.local/iot/');
    check(res, {
        'status is 200': (r) => r.status === 200,
    });
}