// set up socket
const socket = io();
socket.on('connect', () => {

});

const mic = document.getElementById('mic');
const play = document.getElementById('play');
const wordsIn = document.getElementById('wordsIn');
const send = document.getElementById('send');
const speak = document.getElementById('speak');


// user color selection
const color_burgundy = document.getElementById('color_burgundy');
const color_champagne = document.getElementById('color_champagne');
const color_purple = document.getElementById('color_purple');
const color_dark_blue = document.getElementById('color_dark_blue');
const color_silver = document.getElementById('color_silver');
const color_beige = document.getElementById('color_beige');

color_burgundy.onclick = () => {
  socket.emit('speak', "This is color burgundy for dance night" )
}

color_champagne.onclick = () => {
  socket.emit('speak', "This is color champagne for both dance night and wedding" )
}

color_purple.onclick = () => {
  socket.emit('speak', "This is color purple for dance night" )
}

color_dark_blue.onclick = () => {
  socket.emit('speak', "This is color dark blue for dance night" )
}

color_silver.onclick = () => {
  socket.emit('speak', "This is color silver for wedding and dance night" )
}

color_beige.onclick = () => {
  socket.emit('speak', "This is color beige for wedding" )
}

// Assistant speak sentence, microphone listen
speak.onclick = () => {
  socket.emit('speak', wordsIn.value)
  wordsIn.value = ''
}

wordsIn.onkeyup = (e) => { if (e.keyCode === 13) { speak.click(); } };


const src = mic.src
mic.src = ''

play.onclick = () => {
  if(mic.paused) {
  console.log('redo audio')
  mic.src = src
  mic.play()
  play.innerText='end'
  } else {
    mic.pause()
      mic.src = '';
    play.innerText='start'
  }
  
}

setInterval(() => {
  socket.emit('ping-gps', 'dat')
}, 100)
//

// disconnect socket
socket.on('disconnect', () => {
  console.log('disconnect')
  mic.src = ''

  });

var vlSpec = {
  $schema: 'https://vega.github.io/schema/vega-lite/v5.json',
  data: {name: 'table'},
  width: 400,
  mark: 'line',
  encoding: {
    x: {field: 'x', type: 'quantitative', scale: {zero: false}},
    y: {field: 'y', type: 'quantitative'},
    color: {field: 'category', type: 'nominal'}
  }
};

vegaEmbed('#chart', vlSpec).then( (res) => {
  let  x, y, z;
  let counter = -1;
  let cat = ['x', 'y', 'z']
  let minimumX = -100;
   socket.on('pong-gps', (new_x,new_y,new_z) => {
    counter++;
    minimumX++;
    const newVals = [new_x, new_y, new_z].map((c,v) => {
      return {
      x: counter,
      y: c,
      category: cat[v]
    };
  })
    const changeSet = vega
      .changeset()
      .insert(newVals)
      .remove( (t) => {
        return t.x < minimumX;
      });
    res.view.change('table', changeSet).run();
  })

})
