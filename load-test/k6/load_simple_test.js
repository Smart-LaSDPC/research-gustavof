// k6 run load_simple_test.js
import http from 'k6/http';
import { check } from 'k6';

export let options = {
    vus: 10,        // Number of concurrent users
    iterations: 1000,  // Total number of requests to make
    duration: '6000s',  // Time limit (e.g., '30s', '1m', '1h')
};

export default function () {
    const res = http.get('http://iot-api.local/iot/');
    // const res = http.get('http://localhost:8000/health');
    check(res, {
        'status is 200': (r) => r.status === 200,
    });
}