module Jekyll
    class SeoTag
      class Drop < Jekyll::Drops::Drop
        include Jekyll::SeoTag::UrlHelper
        alias_method :orig_canonical_url, :canonical_url
        def canonical_url
          @canonical_url ||= begin
            if page["canonical_url"].to_s.empty?
              filters.absolute_url(page["url"]).to_s.gsub(%r!\.html$!, "")
            else
              page["canonical_url"]
            end
          end
        end
      end
    end
  end