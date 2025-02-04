import http from 'k6/http';
import { sleep } from 'k6';

const vmName = __ENV.VM_NAME;

export let options = {
  vus: 40,
  duration: '12s',
};


export default function () {
  let res = http.get('http://10.1.1.21:30080/iot', {
    headers: { Host: 'iot-api' }
  });
  sleep(1);
}