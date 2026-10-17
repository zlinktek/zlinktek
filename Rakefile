task :default => %i[build]

task :products do
  sh ENV.fetch('PYTHON', Gem.win_platform? ? 'python' : 'python3'), 'scripts/generate-products.py', 'all'
end

task :build => :products do
  sh 'jekyll build --profile --trace --config _config.yml,_config.dev.yml'
end
