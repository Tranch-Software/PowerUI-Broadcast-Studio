var stream;
var peer;
var connectedClient;
var peers = [];
const sUsrAg = navigator.userAgent;

async function createChannel(channelID) {
  if (sUsrAg.indexOf("Firefox") > -1) {
    console.log("Firefox");
    stream = document.getElementById("broadcast").mozCaptureStream();
  } else {
    console.log("Other");
    stream = document.getElementById("broadcast").captureStream();
  }
  document.getElementById("broadcast").play();
  channelID = channelID.replace(/[^a-zA-Z0-9]/g, "_");
  peer = new Peer(channelID);
  peer.on("open", function (id) {
    console.log("Channel " + id + " has been opened.");
  });
  peer.on("connection", function (conn) {
    var connected = conn.peer;
    peers.push(conn);
    console.log(peers);
    connectedClient = conn;
    console.log(
      "User with client ID " + connected + " is viewing the channel."
    );
    conn.on("data", function (data) {
      console.log("Data received: " + data);
      if (data == "stream connect") {
        peer.call(connected, stream);
      } else if (data == "stream exists") {
        console.log("Returning True");
        conn.send("True");
      } else {
        sendAll(data);
      }
    });
  });
}

async function changeStreamSource(srcFile) {
  document.getElementById("broadcast").src = srcFile;
  if (sUsrAg.indexOf("Firefox") > -1) {
    console.log("Firefox");
    stream = document.getElementById("broadcast").mozCaptureStream();
  } else {
    console.log("Other");
    stream = document.getElementById("broadcast").captureStream();
  }
  await callAll();
  document.getElementById("broadcast").play();
}

function callAll() {
  var currentPeers = [];
  for (var i = 0; i < peers.length; i++) {
    currentPeers.push(peers[i]);
    peers.splice(i, 1);
    i--;
  }

  for (var i in currentPeers) {
    currentPeers[i].send("source change");
  }
  return;
}

function sendAll(message) {
  for (var i in peers) {
    peers[i].send(message);
  }
}
