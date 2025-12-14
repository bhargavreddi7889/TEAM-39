module.exports = {
  apps: [
    {
      name: 'chitbox-api',
      script: '.venv/bin/python',
      args: '-m uvicorn src.main:app --host 0.0.0.0 --port 9000',
      cwd: '/home/ubuntu/htdocs/chit/chitbox',
      interpreter: 'none',
      instances: 1,
      autorestart: false,
      watch: false,
      max_memory_restart: '1G',
      kill_timeout: 3000,
      env: {
        PYTHONPATH: '/home/ubuntu/htdocs/chit/chitbox',
        VIRTUAL_ENV: '/home/ubuntu/htdocs/chit/chitbox/.venv',
        PATH: '/home/ubuntu/htdocs/chit/chitbox/.venv/bin:' + process.env.PATH,
      },
      error_file: './logs/api-error.log',
      out_file: './logs/api-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    },
    {
      name: 'chitbox-ui',
      script: '.venv/bin/python',
      args: '-m streamlit run src/app_ui.py --server.port 8501 --server.headless true',
      cwd: '/home/ubuntu/htdocs/chit/chitbox',
      interpreter: 'none',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      kill_timeout: 3000,
      env: {
        PYTHONPATH: '/home/ubuntu/htdocs/chit/chitbox',
        VIRTUAL_ENV: '/home/ubuntu/htdocs/chit/chitbox/.venv',
        PATH: '/home/ubuntu/htdocs/chit/chitbox/.venv/bin:' + process.env.PATH,
      },
      error_file: './logs/ui-error.log',
      out_file: './logs/ui-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    }
  ]
};

