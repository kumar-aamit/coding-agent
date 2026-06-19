
---
apiVersion: v1
kind: Service
metadata:
  name: team-2
  namespace: team-2
  labels:
    app: team-2
spec:
  selector:
    app: team-2
  ports:
    - name: http
      port: 8742
      targetPort: http
---
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: team-2
  namespace: team-2
  labels:
    app: team-2
spec:
  to:
    kind: Service
    name: team-2
    weight: 100
  port:
    targetPort: http
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
