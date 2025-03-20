name: Update AMI

sources:
{{- range $key, $ami := .amis }}
  src_{{ $key }}:
    kind: aws/ami
    spec:
      region: {{ requiredEnv "AWS_REGION" }}
      filters:
        - name: "owner-id"
          values: '{{ $ami.owner_id | default "*" }}'
        - name: "name"
          values: '{{ $ami.pattern }}'
        - name: "architecture"
          values: '{{ $ami.architecture | default "x86_64" }}'
        - name: "block-device-mapping.volume-type"
          values: '{{ $ami.volume_type | default "gp3" }}'
  src_name_{{ $key }}:
    kind: shell
    dependson:
      - src_{{ $key }}
    spec:
      command: aws ec2 describe-images --region {{ requiredEnv "AWS_REGION" }} --image-ids {{ source (printf "src_%s" $key) }} --query 'Images[0].Name' --output text
      environments:
        - name: PATH
        - name: AWS_ACCESS_KEY_ID
        - name: AWS_SECRET_ACCESS_KEY
{{- end }}

targets:
{{- range $key, $target := .targets }}
  yml_{{ $key }}:
    name: {{ $target.source }} bump
    kind: yaml
    sourceid: src_{{ $target.source }}
    scmid: "github"
    spec:
      engine: yamlpath # https://github.com/updatecli/updatecli/issues/4490
      file: '{{ $target.file }}'
      key: '{{ $target.key }}'
      comment: '{{ source (printf "src_name_%s" $target.source) }}'
{{- end }}

actions:
  pr:
    kind: "github/pullrequest"
    scmid: "github"
    spec:
      title: "Bump AMIs versions"
      labels:
        - "updatecli"
        - "ec2-test"

scms:
  github:
    kind: "github"
    spec:
      owner: "Alfresco"
      repository: "alfresco-ansible-deployment"
      branch: "master"
      token: {{ requiredEnv "UPDATECLI_GITHUB_TOKEN" }}
      username: {{ requiredEnv "UPDATECLI_GITHUB_USERNAME" }}
      user: {{ requiredEnv "UPDATECLI_GITHUB_USERNAME" }}
      email: {{ requiredEnv "UPDATECLI_GITHUB_EMAIL" }}
