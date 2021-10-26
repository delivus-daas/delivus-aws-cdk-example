def get_build_spec():

    # Creating new custom Policies
    build_spec = """version: 0.1
frontend:
  phases:
    preBuild:
      commands:
        - yarn install
    build:
      commands:
        - yarn run build
  artifacts:
    baseDirectory: build
    files:
      - '**/*'
  cache:
    paths:
      - node_modules/**/*
"""

    return build_spec
