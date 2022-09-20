package httpapi.authz

default allowed := false

allowed {
    resources := data[input.role][input.action]
    some v
    resources[v] == input.path
}

allowed {
    input.role == "sajang-nim"
}
