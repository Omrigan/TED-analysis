#!/usr/bin/env bash
docker build -t go-to-hack .
docker stop go-to-hack
docker rm go-to-hack
docker run --restart=always -d --name go-to-hack go-to-hack