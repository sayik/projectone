import {h, text, app} from "https://cdn.skypack.dev/hyperapp"

const API_DOMAIN = `http://localhost:5000/`

const putJson = (dispatch, options) => {
  fetch(options.url, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(options.data)
  })
  .then(response => response.json())
  .then(data => dispatch(options.action, data))
}

const fetchJson = (dispatch, options) => {
  fetch(options.url)
  .then(response => response.json())
  .then(data => dispatch(options.action, data))
}

const GotCounter = (state, data) => ({...state, count: data.counter})

const jsonFetcher = (url, action) => [fetchJson, {url, action}]


const updateCounter = (state) => [
  {...state},
  [
    putJson,
    {
      url: API_DOMAIN+"counter/increment",
      action: GotCounter,
      data: {}
    }
  ]
]

const initState = (state) => [
  { count: null },
  jsonFetcher(API_DOMAIN+"counter/read", GotCounter)
]

app({
  init: initState,
  view: state => h("main", {}, [
    h("div", {class: "person"}, [
      h("p", {}, text(`Count ${state.count}`)),
      h("input", {
        type: "button",
        value: "increment",
        onclick: updateCounter,
      }),
    ]),
  ]),
  node: document.getElementById("app"),
})