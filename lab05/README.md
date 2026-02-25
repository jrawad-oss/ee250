# Lab 5

## Team Members
- team member 1
- team member 2

## Lab Question Answers

Answer for Question 1: 
A dBm is a unit of power that describes the received signal strength power in decibals (=1 milliwatt). Values closer to 0 (>-50) are 
considered really good, and values more negative are considered bad (<-80). Generally, ~-67 is good.

Answer for Question 2:
We need to check the OS because different operating systems use different languages, resulting in different system commands and report formats. Linux reports the signal level in dBm 
directly using tools like iwconfig, Windows in percentage using netsh, and MacOS in dBm using its own utlities.

Answer for Question 3:
subprocess.check_output runs a command and returns the output of that command into encoded bytes after it runs completely, 
so that the python script can parse the numbers into a string. It will raise an exception if the command fails.

Answer for Question 4:
re.search uses the argument pattern to scan for its match in the provided string and returns the 
match object. Otherwise, return None.

Answer for Question 5:
In the Windows case, we need to convert the signal quality to dBm because it reports the signal 
quality as a percentage, but Linux reports RSSI in dBm. We do this for consistency and comparison.

Answer for Question 6:
A standard deviation is a quantitative measure for how spread out the data is from the mean. 
It is useful because a location with a high standard deviation tells us that the RSSI mean 
held more signal fluctuation than a location with low standard deviation.

Answer for Question 7:
A dataframe is a two-dimensional labeled data structure that allows for arithmetic operations
and integrates well with plotting libraries. It is useful because it organizes the location, 
mean signal strength, and standard deviations in an organized manner for easy assessment.

Answer for Question 8:
It is important to plot the error bars because they tell us how much the signal varies against the mean.
It helps us understand the stability of the signal at each location and evaluate their differences in
accordance to their signal variability.

Answer for Question 9:
From the plot, the bedroom appears to have the greatest signal strength with a mean of approximately 
-50 dBm, followed by the living room at approximately -60 dBm, both holding the highest reliability. 
Then the bathroom and balcony follow as weaker signals with values at approximately -67 to -69 dBm, 
ending with the kitchen as the weakest signal at approximately -71 dBm. The signal strength becomes 
weaker as the location gets increasingly farther or more obstructed from the router. 
The standard deviation tells us that each signal strength is fairly stable at each spot.

Answers from the Lab Manual:
1) As distance increases, both TCP and UDP throughput generally decrease and becomes more variable. At 2 m, TCP throughput is high at ~35–40 Mbps, then at 4–6 m, it drops to around ~10–20 Mbps, then finally at 8 m, it drops significantly to below 3 Mbps. The same is true for UDP, but at shorter distances, the throughput is rather stable at 10 Mbps, but when it reaches 8 m, it drops significantly, reaching below 1 Mbps in several runs.
2) UDP throughout begins to decrease at around 6 m dropping below 10 Mbps to around 7 Mbps but is very noticeable at 8 m, reaching below 1 Mbps.
3) UDP experiences more packet loss than TCP because, unlike TCP, it lacks congestion control, acknowledgements, or any retransmission to ensure reliable delivery of packets. It maintains a “best effort” delivery system, which just transmits packets without checking for successful delivery or addressing shortcomings.
4) If we increase the UDP bandwidth to -b 100M, then the sender will transmit data at such bandwidth, which may lead to problems arising from the possibility of the wireless link not being able to sustain that bandwidth, especially at larger distances. This would likely lead to increased packet loss and lower throughput. 
5) Yes, the performance would be different on 5 GHz Wi-Fi vs. 2.4 GHz, because the former would likely have a higher throughput at shorter distances whereas the latter would outperform at larger distances. This comes from the fact that 5 GHz operates at a higher frequency, enabling higher data rates, though with a shorter range and weaker wall penetration. 2.4 GHz operates at a lower frequency, meaning signals can travel farther and better through walls but with lower speeds and possible interference between neighboring devices

...
