/*============================================================================
  KWSys - Kitware System Library
  Copyright 2000-2009 Kitware, Inc., Insight Software Consortium

  Distributed under the OSI-approved BSD License (the "License");
  see accompanying file Copyright.txt for details.

  This software is distributed WITHOUT ANY WARRANTY; without even the
  implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
  See the License for more information.
============================================================================*/
#ifndef cmsys_Registry_hxx
#define cmsys_Registry_hxx

#include <cmsys/Configure.h>

#include <cmsys/stl/string>

namespace cmsys
{

class RegistryHelper;

/** \class Registry
 * \brief Portable registry class
 *
 * This class abstracts the storing of data that can be restored
 * when the program executes again. On Win32 platform it is
 * implemented using the registry and on unix as a file in
 * the user's home directory.
 */
class cmsys_EXPORT Registry
{
public:
  enum RegistryType
    {
#ifdef _WIN32
    WIN32_REGISTRY,
#endif
    FILE_REGISTRY
    };

#ifdef _WIN32
  Registry(RegistryType registryType = WIN32_REGISTRY);
#else
  Registry(RegistryType registryType = FILE_REGISTRY);
#endif

  virtual ~Registry();

  //! Read a value from the registry.
  bool ReadValue(const char *subkey, const char *key, const char **value);

  //! Delete a key from the registry.
  bool DeleteKey(const char *subkey, const char *key);

  //! Delete a value from a given key.
  bool DeleteValue(const char *subkey, const char *key);

  //! Set value in a given key.
  bool SetValue(const char *subkey, const char *key,
               const char *value);

  //! Open the registry at toplevel/subkey.
  bool Open(const char *toplevel, const char *subkey,
           int readonly);

  //! Close the registry.
  bool Close();

  //! Read from local or global scope. On Windows this mean from local machine
  // or local user. On unix this will read from $HOME/.Projectrc or
  // /etc/Project
  void GlobalScopeOn() { this->SetGlobalScope(1); }
  void GlobalScopeOff() { this->SetGlobalScope(0); }
  void SetGlobalScope(bool b);
  bool GetGlobalScope();

  // Set or get the toplevel registry key.
  void SetTopLevel(const char* tl);
  const char* GetTopLevel();

  // Return true if registry opened
  bool GetOpened() { return m_Opened; }

  // Should the registry be locked?
  bool GetLocked() { return m_Locked; }

  enum {
    READONLY,
    READWRITE
  };

  // Return true if the character is space.
  int IsSpace(char c);

private:
  RegistryHelper* Helper;

  bool m_Opened;

  bool m_Locked;
}; // End Class: Registry

} // namespace cmsys

#endif
