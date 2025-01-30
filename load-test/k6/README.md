## https://k6.io/docs/get-started/installation/

### Mac
brew install k6


### Debian/Ubuntu

 ```
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

or

snap install k6
 ```


#### Run K6 player load test script
 ```
 k6 run ac.js
 ```
### Debug mode
To enable the debug mode put the following parameter into the command line
 ```
--http-debug="full"
 ```

#### Explanation:
##### Normal Distribution: Simulates requests with intervals following a bell curve, mostly around the mean but with some variation.
##### Uniform Distribution: Simulates requests with equal probability within a specified range, ensuring a steady load.
##### Poisson Distribution: Simulates events occurring randomly over a fixed time period, often used for modeling bursty traffic.
