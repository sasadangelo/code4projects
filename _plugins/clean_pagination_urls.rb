# jekyll-paginate-v2 exposes page paths ending in "index.html", which
# jekyll-seo-tag copies into <link rel="prev/next">. Strip it so crawlers
# only see the canonical trailing-slash URLs (e.g. /tag/aws/page/2/).
Jekyll::Hooks.register [:pages, :documents], :post_render do |doc|
  next unless doc.output_ext == ".html"

  doc.output = doc.output.gsub(%r{(<link rel="(?:prev|next)" href="[^"]*/)index\.html"}, '\1"')
end
