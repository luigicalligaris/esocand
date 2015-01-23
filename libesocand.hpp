#ifndef esocand__libesocand__hpp
#define esocand__libesocand__hpp

#include <string>
#include <vector>
#include <iterator>
#include <random>
#include <algorithm>
#include <functional>

#include <openssl/sha.h>

namespace esocand
{
	class SHA1Hash
	{
		SHA1Hash ()                   {for (size_t i = 0u; i < SHA_DIGEST_LENGTH; ++i) digest[i] = 0u;}
		SHA1Hash (unsigned char * md) {for (size_t i = 0u; i < SHA_DIGEST_LENGTH; ++i) digest[i] = md[i];}
		SHA1Hash (SHA1Hash const& rhs){for (size_t i = 0u; i < SHA_DIGEST_LENGTH; ++i) digest[i] = rhs.digest[i];}
		
		SHA1Hash& operator=(SHA1Hash const& rhs){for (size_t i = 0u; i < SHA_DIGEST_LENGTH; ++i) digest[i] = rhs.digest[i]; return *this;}
		
		bool operator==(SHA1Hash const& rhs)
		{
			for (size_t i = 0u; i < SHA_DIGEST_LENGTH; ++i) if (digest[i] != rhs.digest[i])
				return false;
			return true;
		}
		
		operator size_t()
		{
			size_t result = 0;
			
			for (size_t i = 0; i < SHA_DIGEST_LENGTH; ++i)
			{
				result = result ^ ( size_t(digest[i]) << 8 * ((i * sizeof(unsigned char)) % sizeof(size_t)) );
			}
			
		}
		
		~SHA1Hash(){}
		
		unsigned char digest[SHA_DIGEST_LENGTH];
	}
	
	
	class EsocandShuffler
	{
	public:
		explicit EsocandShuffler(std::string seed_string)
		{
			_seed_string = seed_string;
		}
		
		~EsocandShuffler()
		{
			
		}
		
		void ResetSeedString(std::string seed_string)
		{
			_seed_string = seed_string;
		}
		
		
		
		template <typename T> GetObjectHash(T const& object)
		{
			unsigned char hash_as_chars[SHA_DIGEST_LENGTH];
			SHA_CTX *c;
			SHA_Init(c);
			SHA_Update(c, &object, sizeof(object));
			SHA_Final(&hash_as_chars, c);
			
		}
		
		template <typename T, template <typename,typename = std::allocator<T> > class C = std::vector>
		C< T > GetContainerHash( C< T >& containerToHash )
		{
			
		}
		
		template <typename T, template <typename,typename = std::allocator<T> > class C = std::vector>
		C< T > GetShuffledCopy( C< T >& containerToShuffle )
		{
			C< T > outputContainer(containerToShuffle);
			
			// Default STL sort
			// TODO: is that portable?
			std::sort(outputContainer.begin(), outputContainer.end());
			
			
			
			return outputContainer;
		}
		
	private:
		std::string _seed_string;
	};
	
	
};

#endif