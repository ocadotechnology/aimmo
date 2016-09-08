#!/usr/bin/env bash
set -e
kubectl delete rc aimmo-game-creator || true
sleep 10
kubectl delete rc -l app=aimmo-game
sleep 10
kubectl delete pod -l app=aimmo-game-worker
kubectl delete service -l app=aimmo-game
kubectl create secret generic creator --from-literal=auth=${DJANGO_CREATOR_AUTH_TOKEN}
sleep 5
kubectl create -f rc-aimmo-game-creator.yaml
sleep 10
kubectl get rc
kubectl get pod
kubectl get service
kubectl get ingress
